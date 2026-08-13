<?php
$title      = 'conaboy/publications';
$breadcrumb = '<a href="index.php" style="color:#0000FF">home</a>/<a href="bib.php" style="color:#0000FF">publications</a>';
include __DIR__ . '/includes/header.php';
?>
      <div class="papers">
        <p>
          Publications are listed below (see also <a href="https://ui.adsabs.harvard.edu/search/q=%20author%3A%22conaboy%2C%20luke%22&sort=date%20desc%2C%20bibcode%20desc&p_=0">ADS</a>).
        </p>
        <p>
        </p>
        <?php include('bibtab.html'); ?>
        <p style="font-size: 14px">
          Thanks to <a href=https://garrethmartin.github.io/>Garreth Martin</a>.
        </p>
      </div>
<?php include __DIR__ . '/includes/footer.php'; ?>
