#!/bin/bash

# Script para inicializar o dispositivo GNSS no Linux
# Configura o dispositivo, ativa se necessário, verifica saída e ajusta baud rate

# Configurações padrão - ajuste conforme necessário
DEVICE="/dev/ttyUSB0"
BAUD_RATE="9600"

# Função para verificar se o dispositivo existe
check_device() {
  if [ -e "$DEVICE" ]; then
    echo "Dispositivo GNSS encontrado em $DEVICE"
    return 0
  else
    echo "Dispositivo GNSS não encontrado em $DEVICE"
    return 1
  fi
}

# Função para ativar o dispositivo (exemplo genérico)
activate_device() {
  echo "Tentando ativar o dispositivo GNSS..."
  # Exemplo: carregar módulo do kernel (ajuste conforme seu hardware)
  sudo modprobe usbserial
  sudo modprobe ftdi_sio
  # Aguarda um momento para o dispositivo ser reconhecido
  sleep 2
}

# Função para configurar o baud rate
configure_baud_rate() {
  echo "Configurando baud rate para $BAUD_RATE em $DEVICE"
  stty -F "$DEVICE" "$BAUD_RATE"
}

# Função para verificar a saída do dispositivo
check_output() {
  echo "Verificando saída do dispositivo GNSS (10 segundos)..."
  timeout 10 cat "$DEVICE"
}

# Execução principal
if ! check_device; then
  activate_device
  if ! check_device; then
    echo "Falha ao ativar o dispositivo GNSS. Verifique a conexão."
    exit 1
  fi
fi

configure_baud_rate
check_output

echo "Inicialização do GNSS concluída."
