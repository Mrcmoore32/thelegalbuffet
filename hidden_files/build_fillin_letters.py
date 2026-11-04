#!/usr/bin/env python3
"""Make the letters-page templates fill-in on the page (Craig, 2026-11-04).

- Every [bracketed spot] inside .letter-body becomes a contenteditable span:
  click it and type; focus selects the placeholder so typing replaces it.
- Untouched spots print as blank lines (JS adds .fill-blank at beforeprint;
  print CSS makes the text transparent over an underline) so the printed
  letter can also be filled in BY HAND — Craig's explicit requirement.
- Nothing typed is saved, sent, or collected: pure client-side editing.
- How-to intro rewritten to explain both paths; per-letter tip line added
  (hidden when printing); CSS + JS support added; asset versions bumped.
"""
import re, os, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETTERS = os.path.join(SITE, "letters.html")
CSS = os.path.join(SITE, "assets", "css", "styles.css")
JS = os.path.join(SITE, "assets", "js", "site.js")

TIP = ('<p class="letter-tip">Tip: click the [bracketed spots] in the letter and type '
       'your own words right here &mdash; or print the letter and fill in the blank '
       'lines by hand. Nothing you type is saved, sent, or collected.</p>\n      ')

OLD_HOWTO = ('<strong>How to use any letter on this page:</strong> copy it into an email or a document, '
             'replace every [bracketed blank] with your own details, keep a copy for yourself, and send it '
             'in a way you can prove &mdash; certified mail with return receipt, or email where you keep '
             'the sent copy.')
NEW_HOWTO = ('<strong>How to use any letter on this page:</strong> click any [bracketed spot] and type '
             'your own words right on this page &mdash; nothing you type is saved, sent, or collected &mdash; '
             'then copy the letter or print it finished. Prefer pen and paper? Print it without typing and '
             'every spot comes out as a blank line to fill in by hand. Either way, keep a copy for yourself, '
             'and send it in a way you can prove &mdash; certified mail with return receipt, or email where '
             'you keep the sent copy.')

def main():
    raw = open(LETTERS, encoding="utf-8").read()
    assert OLD_HOWTO in raw, "how-to text not found"
    raw = raw.replace(OLD_HOWTO, NEW_HOWTO, 1)

    span_total = 0
    def fix_body(m):
        nonlocal span_total
        body = m.group(1)
        assert "<div" not in body, "nested div inside letter-body"
        def wrap(mm):
            nonlocal span_total
            ph = mm.group(0)
            assert '"' not in ph, f"quote inside placeholder: {ph}"
            span_total += 1
            return (f'<span class="fill" contenteditable="true" spellcheck="false" '
                    f'data-ph="{ph}">{ph}</span>')
        return '<div class="letter-body">' + re.sub(r"\[[^\]]*\]", wrap, body) + "</div>"

    raw, n_bodies = re.subn(r'<div class="letter-body">(.*?)</div>', fix_body, raw, flags=re.S)
    assert n_bodies == 6, f"expected 6 letter bodies, got {n_bodies}"

    raw, n_tips = re.subn(r'(<div class="letter-body">)',
                          lambda m: TIP + m.group(1), raw)
    assert n_tips == 6, f"expected 6 tips, got {n_tips}"

    raw = raw.replace('assets/css/styles.css?v=20261101a', 'assets/css/styles.css?v=20261104a')
    raw = raw.replace('assets/js/site.js?v=20261101a', 'assets/js/site.js?v=20261104a')
    assert 'styles.css?v=20261104a' in raw and 'site.js?v=20261104a' in raw
    open(LETTERS, "w", encoding="utf-8").write(raw)
    print(f"letters.html: {span_total} fill-in spots wrapped, 6 tips, how-to updated")

    css = open(CSS, encoding="utf-8").read()
    anchor = ".letter-body p { margin: 0 0 1rem; }"
    assert anchor in css and ".fill {" not in css
    css = css.replace(anchor, anchor + """
.letter-tip { background: #fdf6e3; border: 1px dashed var(--accent); border-radius: var(--radius-sm); padding: .6rem .9rem; font-size: .95rem; }
.fill { background: rgba(181,138,67,.16); border-bottom: 1px dashed var(--accent); border-radius: 2px; padding: 0 2px; cursor: text; }
.fill:focus { outline: 2px solid var(--accent); background: #fdf6e3; }""", 1)
    old_hide = "body.printing-letter .letter-actions, body.printing-letter .back-to-top, body.printing-letter .action-plan-bar { display: none !important; }"
    assert old_hide in css
    css = css.replace(old_hide,
        "body.printing-letter .letter-actions, body.printing-letter .back-to-top, body.printing-letter .action-plan-bar, body.printing-letter .letter-tip, body.printing-letter .disclaimer { display: none !important; }\n"
        "  .fill { background: transparent !important; border-bottom: 1px solid #555; display: inline-block; min-width: 5em; }\n"
        "  .fill-blank { color: transparent !important; }", 1)
    open(CSS, "w", encoding="utf-8").write(css)
    print("styles.css: .fill + .letter-tip + print rules added")

    js = open(JS, encoding="utf-8").read()
    anchor_js = '  document.querySelectorAll("[data-print-letter]").forEach(function (btn) {'
    assert anchor_js in js and "fill-blank" not in js
    addition = '''  /* Fill-in letter spots (added 2026-11-04): click a [bracketed spot] and type;
     untouched or emptied spots print as blank lines for filling in by hand. */
  var fills = document.querySelectorAll(".letter-body .fill");
  fills.forEach(function (f) {
    f.addEventListener("focus", function () {
      var r = document.createRange(); r.selectNodeContents(f);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    });
    f.addEventListener("paste", function (e) {
      e.preventDefault();
      var t = (e.clipboardData || window.clipboardData).getData("text");
      document.execCommand("insertText", false, t);
    });
  });
  window.addEventListener("beforeprint", function () {
    fills.forEach(function (f) {
      var t = f.textContent.trim();
      f.classList.toggle("fill-blank", t === "" || t === (f.getAttribute("data-ph") || "").trim());
    });
  });
'''
    js = js.replace(anchor_js, addition + anchor_js, 1)
    open(JS, "w", encoding="utf-8").write(js)
    print("site.js: fill-in behavior added")
    print("OK")

if __name__ == "__main__":
    main()
