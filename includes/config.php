<?php
// Site-wide settings. Edit these in one place instead of every page.

define('SITE_NAME', 'Conaboy');
define('SITE_EMAIL', 'luke.conaboy@nottingham.ac.uk');
define('SITE_CV_URL', 'https://raw.githubusercontent.com/lconaboy/cv/main/cv.pdf');
define('SITE_GITHUB_URL', 'https://github.com/lconaboy');
define('SITE_ADS_URL', 'https://ui.adsabs.harvard.edu/search/q=%20author%3A%22conaboy%2C%20luke%22&sort=date%20desc%2C%20bibcode%20desc&p_=0');

// Single source of truth for the menu bar. Add/remove/reorder links here
// and every page picks up the change automatically.
$SITE_NAV = [
    ['label' => 'home',         'href' => 'index.php',        'color' => '#440154'],
    ['label' => 'cv',           'href' => SITE_CV_URL,        'color' => '#46327E'],
    ['label' => 'talks',        'href' => 'talks.php',        'color' => '#365C8D'],
    ['label' => 'email',        'href' => 'mailto:' . SITE_EMAIL, 'color' => '#277F8E'],
    ['label' => 'github',       'href' => SITE_GITHUB_URL,    'color' => '#1FA187'],
    ['label' => 'publications', 'href' => 'bib.php',          'color' => '#4AC16D'],
    ['label' => 'now-playing', 'href' => 'now-playing.php',          'color' => '#648FFF'],
];
