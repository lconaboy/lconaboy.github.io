    </div><!-- /.container -->

    <div class="footer">
    <div class="text">
    <p style="text-align: center">
    <?php foreach ($SITE_NAV_FOOTER as $link): ?>
      <a href="<?= htmlspecialchars($link['href']) ?>" style="color:<?= htmlspecialchars($link['color']) ?>"><?= htmlspecialchars($link['label']) ?></a>
<?php endforeach; ?>
</p>
</div>
      Updated: <?= date('D d M y') ?>
    </div>

  </div><!-- /.main -->
</body>
</html>
