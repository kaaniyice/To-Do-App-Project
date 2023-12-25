    document.getElementById("todos").addEventListener("click", function(event) {
    const target = event.target;

    if (target.matches("button[id^='edit']")) { // Edit button clicked
        const taskId = target.name;
        const centerDiv = document.getElementById(`centerDIV${taskId}`);
        centerDiv.style.display = centerDiv.style.display === "none" ? "block" : "none";
    } else if (target.matches("input.btClose")) { // Close button clicked
        const taskId = target.id.replace("btClose", "");
        const centerDiv = document.getElementById(`centerDIV${taskId}`);
        centerDiv.style.display = "none"; // Hide the div
    }
});