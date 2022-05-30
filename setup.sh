mkdir -p ~/.streamlit/

echo "\
[server]=0.0.0.0\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml