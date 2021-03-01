# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['var.py'],
             pathex=['E:\\Upwork\\2020\\gmail_app\\gmail_app'],
             binaries=[],
             datas=[('icons/icon.ico', 'imag'), ('icons/mail.ico', 'imag'), ('icons/email.ico', 'imag')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GMonster',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icons\\icon.ico')
