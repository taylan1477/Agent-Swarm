#Requires AutoHotkey v2.0

; Project Jarvis Terminal Automation Shortcuts
; These shortcuts are designed to quickly inject commands into the JetBrains Rider terminal (or any active terminal)

; ::/worker -> Spawns a prompt to assign a task to a worker
::/worker::
(
aider --model gemini/gemini-flash-latest --message "New task assignment: "
)

; ::/master -> Spawns a prompt for the master orchestrator
::/master::
(
aider --model gemini/gemini-flash-latest --message "Analyze this feature request and delegate: "
)

; Win + Alt + S: Start Swarm
#!s::
{
    SendText("./scripts/start_swarm.sh")
    Send("{Enter}")
}

; Win + Alt + M: Query Memory
#!m::
{
    ; Example of a direct memory query (assuming an alias or script exists)
    SendText('echo "Querying MCP memory..."')
    Send("{Enter}")
}
