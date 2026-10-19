const {test} = require('node:test');
const assert = require('node:assert/strict');
const prefs = require('../static/js/preferences.js');

function storage() {
    const values = new Map();
    return {getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value), values};
}

test('defaults and persistence across reloads', () => {
    const store = storage();
    assert.deepEqual(prefs.load(store, ['dushanbe', 'khujand']).value, prefs.defaults);
    const saved = {defaultLocation: 'khujand', refreshMinutes: 5, language: 'tg'};
    prefs.save(store, saved, ['dushanbe', 'khujand']);
    assert.deepEqual(prefs.load(store, ['dushanbe', 'khujand']).value, saved);
    prefs.save(store, prefs.defaults, ['dushanbe', 'khujand']);
    assert.deepEqual(prefs.load(store, ['dushanbe', 'khujand']).value, prefs.defaults);
});

test('invalid controls never persisted', () => {
    const store = storage();
    for (const override of [{refreshMinutes: 0}, {refreshMinutes: Infinity}, {refreshMinutes: '5'},
        {refreshMinutes: 500}, {language: 'unknown'}, {defaultLocation: 'unknown'}]) {
        assert.throws(() => prefs.save(store, {...prefs.defaults, ...override}, ['dushanbe']));
        assert.equal(store.values.size, 0);
    }
});

test('corrupt or blocked storage uses visible fallback and save errors propagate', () => {
    const store = storage();
    store.setItem(prefs.key, 'not json');
    assert.ok(prefs.load(store, ['dushanbe']).warning);
    const denied = {getItem() {throw new Error('blocked');}, setItem() {throw new Error('blocked');}};
    assert.ok(prefs.load(denied, ['dushanbe']).warning);
    assert.throws(() => prefs.save(denied, prefs.defaults, ['dushanbe']), /blocked/);
});

test('only supported non-sensitive preferences stored', () => {
    const store = storage();
    prefs.save(store, {...prefs.defaults, apiKey: 'do-not-store', unrelated: 1}, ['dushanbe']);
    assert.deepEqual(Object.keys(JSON.parse(store.getItem(prefs.key))).sort(), ['defaultLocation', 'language', 'refreshMinutes']);
});
