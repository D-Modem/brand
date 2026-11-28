# Palette, type and the app icon

## Palette

Each core repository has one Rainbow Book. The color of the Book is the accent on
the social preview of the repository. It is also the color of the spine on
the left edge of the preview. The spine shows the full name of the
repository.

| Book | Format | Color | Repository |
| --- | --- | --- | --- |
| Red | CD-DA | `#ff4d5e` | [D-Modem](https://github.com/D-Modem/D-Modem) |
| Orange | CD-R/RW | `#ff8a3d` | [hardware](https://github.com/D-Modem/hardware) |
| Yellow | CD-ROM | `#ffd23d` | [app](https://github.com/D-Modem/app) |
| Green | CD-i | `#3ddc84` | [login](https://github.com/D-Modem/login) |
| Blue | CD Extra | `#3d8bff` | [bbs](https://github.com/D-Modem/bbs) |
| Purple | DDCD | `#a66bff` | Free |
| Scarlet | SACD | `#c8102e` | [gui](https://github.com/D-Modem/gui) |
| White | Video CD | `#f2f4fa` | [brand](https://github.com/D-Modem/brand) |

Purple (DDCD) and Beige (Photo CD) are available for a future core
repository. A support library, for example
[go3270](https://github.com/D-Modem/go3270), does not get a Book.

Neutrals: background `#0a0f1c`, panel `#121a2e`, text `#e8f0ff`, muted
`#7f8bab`. Type: Sauce Code Pro, the [Nerd Fonts](https://www.nerdfonts.com/) build of
[Source Code Pro](https://github.com/adobe-fonts/source-code-pro).

## App icon

<img src="../app-icon/play-store.png" width="160" alt="D-Modem app icon">

The icon is the front of an RJ11 jack, with the white carrier in it. Its
outline has stripes in the Rainbow Book colours, as the mark has. It is drawn
on the 108-unit adaptive icon canvas of Android. The `ic_launcher_foreground`
and `ic_launcher_monochrome` vector drawables of the app follow
`tools/app_icon.py`.
