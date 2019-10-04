var animation = bodymovin.loadAnimation({
    container: document.getElementById('kitty'),
    path: './assets/kitty.json', // Required
    renderer: 'svg',
    loop: true,
    autoplay: true,
    name: "kitty",
  });
