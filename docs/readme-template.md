# README template

Every repository's top-level README is a short landing page. Technical
detail lives in the repository's `docs/` (bbs: `docs/wiki/`), which also
feeds its website.

```markdown
<img src=".github/banner.png" alt="D-Modem/<repo>: <tagline>" width="100%">

# <name>

<one line: what it is>

<two or three sentences: what it does and who it is for>

- <feature>
- <feature>
- <four to six in all>

## Quick start

<install or build in a few lines>

## Documentation

- Website: https://d-modem.github.io/<repo>/
- <the docs index, or the wiki>

## The D-Modem suite

<the shared table of the seven repositories>

## Licence

<one or two lines, linking COPYING or LICENSING.md>
```

Until a repository's website is live, its Documentation section links the
docs index (or the wiki) only.

The suite table, the same in every README:

| Repository | What it is |
| --- | --- |
| [D-Modem](https://github.com/D-Modem/D-Modem) | The open V.92 softmodem: dmodemd, libdmodem and the Asterisk, FreeSWITCH and ARI modules |
| [app](https://github.com/D-Modem/app) | The D-Modem app for Android and iOS: a dial-up modem on a SIP call |
| [hardware](https://github.com/D-Modem/hardware) | pico-serial: RP2040 serial adapters and phone-line USB sticks |
| [menu](https://github.com/D-Modem/menu) | modemmenu: the login and menu dial-up callers reach |
| [bbs](https://github.com/D-Modem/bbs) | A bulletin board for telnet, SSH, TN3270 and modem callers |
| [go3270](https://github.com/D-Modem/go3270) | A Go library for 3270 terminal servers, used by bbs |
| [brand](https://github.com/D-Modem/brand) | Logos, colours, type and the naming guide |
