import polib
import glob
import os

root = os.path.dirname(os.path.dirname(__file__))
po_files = glob.glob(os.path.join(root, 'locale', '*', 'LC_MESSAGES', '*.po'))
if not po_files:
    print('No .po files found under locale/*/LC_MESSAGES')
else:
    for po in po_files:
        mo = os.path.splitext(po)[0] + '.mo'
        print(f'Compiling {po} -> {mo}')
        p = polib.pofile(po)
        p.save_as_mofile(mo)
    print('Done')
