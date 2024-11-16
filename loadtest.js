import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    thresholds: {
        errors: ['rate<0.1'],
    },
    stages: [
        { duration: '1m', target: 10 },
        { duration: '2m', target: 10 },
        { duration: '1m', target: 0 },
    ],
};

export default function () {
    let res;

    res = http.get('http://localhost:8000/products/python');
    check(res, {
        'status was 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    res = http.get('http://localhost:8000/products/python/3.11');
    check(res, {
        'status was 200': (r) => r.status === 200,
        'eol exists': (r) => r.json().eol !== undefined,
    }) || errorRate.add(1);

    res = http.get('http://localhost:8000/products/python/3.11/summarized');
    check(res, {
        'status was 200': (r) => r.status === 200,
        'eol exists': (r) => r.json().eol !== undefined,
    }) || errorRate.add(1);

    sleep(1);
}
