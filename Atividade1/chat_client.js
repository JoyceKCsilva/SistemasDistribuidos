const net = require('net');
const readline = require('readline');

// Configurações do cliente
const HOST = '127.0.0.1'; // Substitua pelo IP do servidor, se necessário
const PORT = 12345;       // Porta do servidor

// Cria uma interface para entrada do terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Conecta ao servidor
const client = net.createConnection({ host: HOST, port: PORT }, () => {
  console.log('[CONECTADO AO SERVIDOR]');
  console.log('Digite mensagens e pressione Enter para enviar.');
});

// Evento: Receber dados do servidor
client.on('data', (data) => {
  console.log(data.toString());
});

// Evento: Encerramento da conexão
client.on('end', () => {
  console.log('[DESCONECTADO DO SERVIDOR]');
  process.exit();
});

// Evento: Erro na conexão
client.on('error', (err) => {
  console.error(`[ERRO]: ${err.message}`);
});

// Lê entrada do usuário e envia para o servidor
rl.on('line', (input) => {
  if (input.toLowerCase() === 'sair') {
    console.log('[DESCONECTANDO...]');
    client.end();
    rl.close();
  } else {
    client.write(input);
  }
});