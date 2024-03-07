<script>
    window.onload = function() {
        document.querySelectorAll('.nav-links').forEach(function(navLinks) {
            navLinks.addEventListener('click', function(event) {
                if (event.target.tagName === 'A') {
                    event.preventDefault();
                    let url = event.target.getAttribute('href');
                    window.location.href = url;
                }
            });
        });
    };
</script>
