document.addEventListener("DOMContentLoaded", function () {
  const clases = [
    '.hero-content',
    '.hero-content1',
    '.hero-content2',
    '.hero-content3',
    '.hero-content4'
  ];

  const elementos = clases.flatMap(clase =>
    Array.from(document.querySelectorAll(clase))
  );

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1
  });

  elementos.forEach(el => observer.observe(el));
});