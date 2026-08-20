from pathlib import Path
source = Path('C:/Users/Pascal/Documents/VSC - GH Repos/Reflections-of-Representations/Reflections.py')
text = source.read_text(encoding='utf-8')
marker = 'st.set_page_config(layout="wide")'
if 'def main():' not in text:
    start = text.index(marker)
    prefix = text[:start]
    body = text[start:]
    indented_body = '\n'.join('    ' + line if line else '' for line in body.splitlines())
    new_text = prefix + 'def main():\n' + indented_body + '\n\nif __name__ == "__main__":\n    main()\n'
    source.write_text(new_text, encoding='utf-8')
    print('refactored')
else:
    print('already wrapped')
