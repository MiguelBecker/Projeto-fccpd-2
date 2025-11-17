echo "Cliente iniciado..."
while true; do
    echo "Requisitando servidor"
    curl http://server:8080
    echo ""
    sleep 3
done
