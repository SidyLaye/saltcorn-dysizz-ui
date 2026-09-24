"""Tests du convertisseur HTML → éléments natifs du builder."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from html2layout import html2layout


class T(unittest.TestCase):
    def test_heading(self):
        s = html2layout('<h2 class="dz-h2">Titre</h2>')
        self.assertEqual(s, {"type": "blank", "contents": "Titre", "customClass": "dz-h2", "textStyle": "h2"})

    def test_button_link_with_icon(self):
        s = html2layout('<a class="dz-btn" href="/x"><i class="fas fa-plus"></i> Créer</a>')
        self.assertEqual(s["type"], "link")
        self.assertEqual(s["link_style"], "dz-btn")
        self.assertEqual(s["link_icon"], "fas fa-plus")
        self.assertEqual(s["text"], "Créer")

    def test_container_keeps_tag_and_classes(self):
        s = html2layout('<section class="dz-card" id="a"><p>Texte</p></section>')
        self.assertEqual(s["htmlElement"], "section")
        self.assertEqual(s["customId"], "a")
        self.assertEqual(s["contents"]["htmlElement"], "p")

    def test_data_attributes_become_classes(self):
        s = html2layout('<div data-dz-reveal="zoom" class="x"><span data-dz-count="48250" data-dz-suffix=" €">0</span></div>')
        self.assertIn("dz-reveal-zoom", s["customClass"])
        self.assertIn("dz-counter", s["contents"]["customClass"])
        self.assertEqual(s["contents"]["contents"], "48 250 €")

    def test_unknown_attribute_stays_code(self):
        s = html2layout('<div data-foo="1">x</div>')
        self.assertTrue(s["isHTML"])

    def test_aria_label_becomes_hidden_text(self):
        s = html2layout('<button class="dz-btn" aria-label="Menu"><i class="fas fa-bars"></i></button>')
        self.assertIn("visually-hidden", s["contents"]["contents"])

    def test_raw_tags(self):
        self.assertTrue(html2layout("<svg><path d='M0'/></svg>")["isHTML"])


if __name__ == "__main__":
    unittest.main()
