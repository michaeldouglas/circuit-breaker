import requests
from pybreaker import CircuitBreaker, CircuitBreakerError

# Configurações do circuit breaker
failure_threshold = 3  # Número máximo de falhas consecutivas permitidas
success_threshold = 5  # Número mínimo de sucessos consecutivos necessários
# Tempo de espera em segundos antes de tentar novamente após o circuit breaker bloquear a chamada
reset_timeout = 3

# Cria o circuit breaker
breaker = CircuitBreaker(fail_max=failure_threshold,
                         reset_timeout=reset_timeout)


@breaker
def call_endpoint():
    response = requests.get('http://localhost:5000/failure')
    response.raise_for_status()  # Lança uma exceção caso a resposta não seja bem-sucedida
    return response.json()


# Executa o loop para testar o circuit breaker
for i in range(1, 11):
    print(f"Executando iteração {i}")

    try:
        result = call_endpoint()
        print('Chamada bem-sucedida!')
        print(f"Resultado: {result}")
    except CircuitBreakerError:
        print('Chamada bloqueada pelo circuit breaker')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao chamar o endpoint: {e}')

    print("---------------------------")

print("Loop concluído!")
