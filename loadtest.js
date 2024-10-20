import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    thresholds: {
        errors: ['rate<0.1'], // Limite de erros para o teste de carga
    },
    stages: [
        { duration: '1m', target: 10 }, // Aumenta para 10 usuários em 1 minuto
        { duration: '2m', target: 10 }, // Mantém 10 usuários por 2 minutos
        { duration: '1m', target: 0 },  // Diminui para 0 usuários em 1 minuto
    ],
};

export default function () {
    let res = http.get('http://localhost:8000/health/liveness');
    check(res, {
        'status was 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    res = http.get('http://localhost:8000/health/readiness');
    check(res, {
        'status was 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    res = http.get('http://localhost:8000/products/all');
    check(res, {
        'status was 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    res = http.get('http://localhost:8000/products/python/3.11');
    check(res, {
        'status was 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    sleep(1);
}
