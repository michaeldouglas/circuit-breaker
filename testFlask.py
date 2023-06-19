from flask import Flask, jsonify
from pybreaker import CircuitBreaker, CircuitBreakerError
import requests

app = Flask(__name__)

# Configurações do circuit breaker
failure_threshold = 3  # Número máximo de falhas consecutivas permitidas
success_threshold = 5  # Número mínimo de sucessos consecutivos necessários
# Tempo de espera em segundos antes de tentar novamente após o circuit breaker bloquear a chamada
reset_timeout = 10

# Cria o circuit breaker
breaker = CircuitBreaker(fail_max=failure_threshold,
                         reset_timeout=reset_timeout)


@breaker
def check_service_status():
    response = requests.get('https://httpstat.us/500')
    if response.status_code == 200:
        return True
    else:
        raise Exception('O serviço está fora do ar!')


@app.route('/status')
def status():
    try:
        check_service_status()
        return jsonify({'status': 'Serviço está funcionando corretamente!'})
    except CircuitBreakerError:
        return jsonify({'status': 'Serviço está com problemas!'})
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route('/service')
def service():
    return jsonify({'data': 'Dados do serviço'})


if __name__ == '__main__':
    app.run(port=8080)
