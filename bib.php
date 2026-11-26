<?php
$title      = 'conaboy/publications';
$breadcrumb = '<a href="index.php" style="color:#0000FF">home</a>/<a href="bib.php" style="color:#0000FF">publications</a>';
include __DIR__ . '/includes/header.php';
?>
      <div class="papers">
        <p>
          Publications are listed below (see also <a href="https://scixplorer.org/search?ads_compat=1&fq=%7B%21type%3Daqp+v%3D%24fq_database%7D&fq_database=%28database%3A%22astronomy%22+OR+database%3A%22physics%22%29&p=1&q=docs%28library%2FnSlRHFo1SuK1_F-NjihsGQ%29&sort=date+desc&d=astrophysics">SciX</a>).
        </p>
        <p>
        </p>
        <?php include('bibtab.html'); ?>
        <p style="font-size: 14px">
          Thanks to <a href=https://garrethmartin.github.io/>Garreth Martin</a>.
        </p>
      </div>
<?php include __DIR__ . '/includes/footer.php'; ?>
