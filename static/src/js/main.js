window.addEventListener("pageshow", function (event) {
    const navigation = performance.getEntriesByType("navigation")[0];

    if (event.persisted || navigation?.type === "back_forward") {
        location.reload();
    }
});