<?php
require_once __DIR__ . '/config.php';

// Every page sets $title (and optionally $breadcrumb) before including this file.
$title = $title ?? SITE_NAME;
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="styles.css">
  <meta name="google-site-verification" content="egpqFBWYXcbmA02K-_elZgx0FR7HUNiZ4mA1jsgvEOs" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= htmlspecialchars($title) ?></title>
</head>
<body>
  <div class="main">

    <div class="header">
<?php foreach ($SITE_NAV as $link): ?>
      <a href="<?= htmlspecialchars($link['href']) ?>" style="color:<?= htmlspecialchars($link['color']) ?>"><?= htmlspecialchars($link['label']) ?></a>
<?php endforeach; ?>
    </div>

    <div class="container">
<?php if (!empty($breadcrumb)): ?>
      <p style="text-align: center">
<?= $breadcrumb /* trusted, page-authored HTML */ ?>
      </p>
<?php endif; ?>
