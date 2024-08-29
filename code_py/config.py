pid_file = "basic.pid"  
core = 'basic.exe'
 
json_add = {
    "fons": """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap" rel="stylesheet">
    """,
    "css": """
        <script src="/static/js/jquery-3.6.4.min.js"></script>    
        <link rel="stylesheet" href="/static/css/index.css">
        <script src="/static/js/global.js"></script>
    """,
    "live_app":"""
    <script>
        function sendHeartbeat() {
            fetch('/heartbeat', { method: 'POST' })
                .then(response => response.json())
                .then(data => console.log('Server response:', data))
                .catch(error => console.error('Error:', error));
        }

        setInterval(sendHeartbeat, 3000);
    </script>
    """
}