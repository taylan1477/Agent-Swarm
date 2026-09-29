#!/bin/bash

# start_swarm.sh
# Initializes the autonomous agent swarm in isolated tmux sessions.

# Ensure tmux is installed
if ! command -v tmux &> /dev/null
then
    echo "tmux could not be found. Please install it (e.g., sudo apt install tmux)."
    exit 1
fi

# Ensure GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Warning: GEMINI_API_KEY is not set in the environment."
    echo "Agents will fail to connect to Gemini 3.1 Pro."
fi

# Session names for the domains
SESSION_MASTER="agent-master"
SESSION_CORE="agent-core"
SESSION_TESTS="agent-tests"

echo "Starting Project Jarvis Swarm..."

# Get current script directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Start master orchestrator
tmux new-session -s $SESSION_MASTER -d
tmux send-keys -t $SESSION_MASTER "cd '$PROJECT_DIR' && [ -f ~/.venvs/jarvis/bin/activate ] && source ~/.venvs/jarvis/bin/activate || ([ -f venv/bin/activate ] && source venv/bin/activate)" C-m
tmux send-keys -t $SESSION_MASTER "echo 'Master Orchestrator initialized. Waiting for tasks...'" C-m
tmux send-keys -t $SESSION_MASTER "aider --model gemini/gemini-flash-latest" C-m

# Start core backend worker
tmux new-session -s $SESSION_CORE -d
tmux send-keys -t $SESSION_CORE "cd '$PROJECT_DIR' && [ -f ~/.venvs/jarvis/bin/activate ] && source ~/.venvs/jarvis/bin/activate || ([ -f venv/bin/activate ] && source venv/bin/activate)" C-m
tmux send-keys -t $SESSION_CORE "echo 'Core Backend Worker initialized.'" C-m
tmux send-keys -t $SESSION_CORE "aider --model gemini/gemini-flash-latest" C-m

# Start test worker
tmux new-session -s $SESSION_TESTS -d
tmux send-keys -t $SESSION_TESTS "cd '$PROJECT_DIR' && [ -f ~/.venvs/jarvis/bin/activate ] && source ~/.venvs/jarvis/bin/activate || ([ -f venv/bin/activate ] && source venv/bin/activate)" C-m
tmux send-keys -t $SESSION_TESTS "echo 'Test Worker initialized.'" C-m
tmux send-keys -t $SESSION_TESTS "aider --model gemini/gemini-flash-latest" C-m

echo "Swarm initialized in tmux sessions!"
echo "Use 'tmux ls' to view active sessions."
echo "Use 'tmux attach -t <session_name>' to connect to a specific agent."
