<?php
/**
 * generate-records.php
 *
 * Run this LOCALLY (not on the server / not published) to fetch your
 * Discogs collection and bake it into a static records.json file.
 *
 * Usage:
 *   DISCOGS_TOKEN=your_token_here php generate-records.php
 *
 * or store the token in a local, gitignored file called `discogs-token.txt`
 * (one line, just the token) next to this script and run:
 *   php generate-records.php
 *
 * The output, records.json, contains no token — it's just your release
 * data — so it's safe to commit and publish alongside nowplaying.php.
 */

$USERNAME = getenv('DISCOGS_USERNAME') ?: null;
if (!$USERNAME) {
    $homeDir = getenv('HOME');
    $usernameFile = "$homeDir/.discogs/discogs-username.txt";
    if (is_file($usernameFile)) {
        $USERNAME = trim(file_get_contents($usernameFile));
    }
}
if (!$USERNAME) {
    fwrite(STDERR, "No Discogs token username found. Set DISCOGS_USERNAME env var or create $HOME/.discogs/discogs-username.txt.\n");
    exit(1);
}


$TOKEN = getenv('DISCOGS_TOKEN') ?: null;
if (!$TOKEN) {
    $homeDir = getenv('HOME');
    $tokenFile = "$homeDir/.discogs/discogs-token.txt";
    if (is_file($tokenFile)) {
        $TOKEN = trim(file_get_contents($tokenFile));
    }
}
if (!$TOKEN) {
    fwrite(STDERR, "No Discogs token found. Set DISCOGS_TOKEN env var or create $HOME/.discogs/discogs-token.txt.\n");
    exit(1);
}

function fetchPage(string $username, string $token, int $page): array {
    $url = sprintf(
        'https://api.discogs.com/users/%s/collection/folders/0/releases?token=%s&per_page=100&sort=artist&page=%d',
        rawurlencode($username),
        rawurlencode($token),
        $page
    );

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 20,
        CURLOPT_HTTPHEADER     => [
            'User-Agent: NowPlayingBuildScript/1.0 +https://example.com',
        ],
    ]);
    $body = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    // curl_close($ch);

    if ($body === false || $code >= 400) {
        fwrite(STDERR, "Request failed (HTTP $code): $err\n");
        exit(1);
    }

    $data = json_decode($body, true);
    if (!isset($data['releases'])) {
        fwrite(STDERR, "Unexpected response shape on page $page.\n");
        exit(1);
    }
    return $data;
}

echo "Fetching page 1…\n";
$first = fetchPage($USERNAME, $TOKEN, 1);
$releases = $first['releases'];
$pages = $first['pagination']['pages'] ?? 1;

for ($p = 2; $p <= $pages; $p++) {
    echo "Fetching page $p of $pages…\n";
    $data = fetchPage($USERNAME, $TOKEN, $p);
    $releases = array_merge($releases, $data['releases']);
}

// Trim each release down to just what the page needs, to keep the
// published JSON small and avoid carrying along any Discogs account
// metadata you don't need public.
$slim = array_map(function ($r) {
    $info = $r['basic_information'];
    return [
        'basic_information' => [
            'id'          => $info['id'] ?? null,
            'master_id'   => $info['master_id'] ?? null,
            'title'       => $info['title'] ?? '',
            'year'        => $info['year'] ?? null,
            'cover_image' => $info['cover_image'] ?? '',
            'thumb'       => $info['thumb'] ?? '',
            'artists'     => array_map(fn($a) => ['name' => $a['name'] ?? ''], $info['artists'] ?? []),
            'formats'     => $info['formats'] ?? [],
        ],
    ];
}, $releases);

$outFile = __DIR__ . '/records.json';
file_put_contents($outFile, json_encode($slim, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));

echo "Wrote " . count($slim) . " releases to $outFile\n";
