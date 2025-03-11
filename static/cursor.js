//site wide cursor
const site_wide_cursor = document.querySelector('.custom-cursor.site-wide');

document.addEventListener('mouseenter', () => {
    site_wide_cursor.style.display = 'block';
});

document.addEventListener('mouseleave', () => {
    site_wide_cursor.style.display = 'none';
});

document.addEventListener('mousemove', TrackCursor)

function TrackCursor (evt) {
    const w = site_wide_cursor.clientWidth
    const h = site_wide_cursor.clientHeight

    site_wide_cursor.style.transform  =  `translate(${evt.clientX -w/2}px, ${evt.clientY -h/2}px)`;
}