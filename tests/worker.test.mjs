// Kiểm thử chatbot Luvetta Gift Assistant (ai-agent/worker.js) bằng AI giả lập.
// Chạy:  node --test tests/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import worker from '../ai-agent/worker.js';

const ORIGIN = 'https://luvetta.store';

function fakeAI(reply) {
  const calls = [];
  return {
    calls,
    async run(model, input) { calls.push({ model, input }); return typeof reply === 'function' ? reply(input) : reply; }
  };
}

function env(ai) {
  return { ALLOWED_ORIGINS: 'https://luvetta.store,https://www.luvetta.store', AI: ai };
}

function post(contents, origin = ORIGIN) {
  return new Request('https://agent.example.workers.dev/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin },
    body: JSON.stringify({ contents })
  });
}

const userSays = (text) => [{ role: 'user', parts: [{ text }] }];

test('GET trả về trạng thái dịch vụ', async () => {
  const r = await worker.fetch(new Request('https://x/', { headers: { Origin: ORIGIN } }), env(fakeAI({})));
  const j = await r.json();
  assert.equal(r.status, 200);
  assert.equal(j.service, 'luvetta-agent');
  assert.equal(j.ai_binding, true);
});

test('chặn website lạ (CORS)', async () => {
  const r = await worker.fetch(post(userSays('hi'), 'https://evil.example'), env(fakeAI({ response: 'x' })));
  assert.equal(r.status, 403);
});

test('preflight OPTIONS từ luvetta.store được phép', async () => {
  const r = await worker.fetch(new Request('https://x/', { method: 'OPTIONS', headers: { Origin: ORIGIN } }), env(fakeAI({})));
  assert.equal(r.status, 204);
  assert.equal(r.headers.get('Access-Control-Allow-Origin'), ORIGIN);
});

test('từ chối dữ liệu sai định dạng', async () => {
  const r = await worker.fetch(post([]), env(fakeAI({})));
  assert.equal(r.status, 400);
});

test('trả lời chữ và gửi kèm system prompt + 4 công cụ', async () => {
  const ai = fakeAI({ response: 'Who is the lucky person? ♡' });
  const r = await worker.fetch(post(userSays('I need a gift for my mom')), env(ai));
  const j = await r.json();
  assert.equal(r.status, 200);
  assert.equal(j.content.parts[0].text, 'Who is the lucky person? ♡');
  const input = ai.calls[0].input;
  assert.equal(input.messages[0].role, 'system');
  assert.match(input.messages[0].content, /Never add anything to the cart without the customer's clear confirmation/);
  assert.deepEqual(input.tools.map(t => t.name).sort(), ['add_to_cart', 'check_options', 'get_store_info', 'view_cart']);
});

test('chuyển tool_calls của model thành functionCall', async () => {
  const ai = fakeAI({ tool_calls: [{ name: 'check_options', arguments: { letter: 'M', color: 'Gold' } }] });
  const r = await worker.fetch(post(userSays('Letter M in gold?')), env(ai));
  const j = await r.json();
  assert.deepEqual(j.content.parts[0].functionCall, { name: 'check_options', args: { letter: 'M', color: 'Gold' } });
});

test('nhận lệnh gọi công cụ dạng chữ JSON', async () => {
  const ai = fakeAI({ response: '{"name":"view_cart","parameters":{}}' });
  const j = await (await worker.fetch(post(userSays("what's in my cart")), env(ai))).json();
  assert.equal(j.content.parts[0].functionCall.name, 'view_cart');
});

test('sau khi có kết quả công cụ thì bắt buộc trả lời bằng chữ (chống lặp)', async () => {
  const ai = fakeAI({ response: 'Letter M in Gold is available for $5 ✨' });
  const contents = [
    ...userSays('Letter M in gold?'),
    { role: 'model', parts: [{ functionCall: { name: 'check_options', args: { letter: 'M', color: 'Gold' } } }] },
    { role: 'user', parts: [{ functionResponse: { name: 'check_options', response: { available: true, price: '5.00' } } }] }
  ];
  await worker.fetch(post(contents), env(ai));
  assert.equal(ai.calls[0].input.tools, undefined);
});

test('báo rate_limited khi hết hạn mức Workers AI', async () => {
  const ai = { async run() { throw new Error('daily neuron limit exceeded'); } };
  const r = await worker.fetch(post(userSays('hi')), env(ai));
  assert.equal(r.status, 429);
  assert.equal((await r.json()).error, 'rate_limited');
});

test('bản worker trong skill luvetta-gift-agent trùng với ai-agent/', () => {
  const a = readFileSync(new URL('../ai-agent/worker.js', import.meta.url), 'utf8');
  const b = readFileSync(new URL('../ai-skills/luvetta-gift-agent/assets/worker.js', import.meta.url), 'utf8');
  assert.equal(a, b);
});
