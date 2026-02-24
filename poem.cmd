@echo off
:: poem.cmd — entrypoint for the poem tool CLI
:: Add the repo root directory to your Windows PATH to call as: poem <command>

cd /d "%~dp0tools"
python poem_tool.py %*
