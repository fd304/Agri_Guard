import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Template(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.labels = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'label':
            self.labels.append(attrs.get('for'))
        if tag == 'script':
            self.scripts.append(attrs.get('src'))


def test_frontend_ids_and_labels_match_application():
    parser = Template()
    parser.feed((ROOT / 'templates/index.html').read_text())
    app = (ROOT / 'static/js/app.js').read_text()
    assert len(parser.ids) == len(set(parser.ids))
    for element_id in re.findall(r"byId\('([^']+)'\)", app):
        assert element_id in parser.ids, element_id
    assert all(label and label in parser.ids for label in parser.labels)
    assert set(parser.scripts) == {'/static/vendor/lucide.js', '/static/js/preferences.js', '/static/js/app.js', '/static/js/charts.js'}
    for script in parser.scripts:
        assert (ROOT / script.lstrip('/')).exists()


def test_no_dynamic_html_or_independent_water_estimate():
    app = (ROOT / 'static/js/app.js').read_text()
    chart = (ROOT / 'static/js/charts.js').read_text()
    assert 'innerHTML' not in app
    assert "data.decision.state === 'IRRIGATE'" in app
    assert 'data.irrigation.amount_mm' in app
    assert 'data.plan' in app
    assert 'day.amount_mm' in chart and 'day.water_liters' in chart
    assert 'ET0 - Rainfall' not in chart
    assert 'setInterval' in app and 'clearInterval' in app
    assert 'refreshMinutes * 60000' in app
    assert 'report_type:' in app and 'period:' in app and 'format:' in app and 'limit}' in app
    assert 'Math.random' not in app
    template = (ROOT / 'templates/index.html').read_text()
    assert '↑ 8%' not in template
    assert '/static/favicon.svg' in template
