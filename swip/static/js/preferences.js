(function(root) {
    'use strict';
    const defaults = Object.freeze({defaultLocation: 'dushanbe', refreshMinutes: 30, language: 'en'});
    const key = 'swip.preferences.v1';
    function validate(candidate, locationIds) {
        if (!candidate || !locationIds.includes(candidate.defaultLocation) ||
            ![5, 15, 30, 60].includes(candidate.refreshMinutes) || !['en', 'ru', 'tg'].includes(candidate.language)) {
            throw new Error('Choose a configured location, refresh interval (5/15/30/60 minutes) and supported language.');
        }
        return {defaultLocation: candidate.defaultLocation, refreshMinutes: candidate.refreshMinutes, language: candidate.language};
    }
    function load(storage, locationIds) {
        try {
            const raw = storage.getItem(key);
            return {value: raw ? validate(JSON.parse(raw), locationIds) : {...defaults}, warning: null};
        } catch (_) {
            return {value: {...defaults}, warning: 'Stored preferences unavailable or invalid. Defaults are active; save to restore persistence.'};
        }
    }
    function save(storage, candidate, locationIds) {
        const value = validate(candidate, locationIds);
        storage.setItem(key, JSON.stringify(value));
        return value;
    }
    const preferences = {defaults, key, validate, load, save};
    if (typeof module !== 'undefined') module.exports = preferences;
    else root.SWIPPreferences = preferences;
})(typeof window === 'undefined' ? globalThis : window);
