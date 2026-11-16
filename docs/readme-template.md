# README template

The top-level README of each repository is a short landing page. Put the
technical details in the `docs/` of the repository (bbs: `docs/wiki/`). The
website of the repository also uses these files. Write the README and the
docs in ASD-STE100 Simplified Technical English ([STYLE.md](STYLE.md)).

```markdown
<img src=".github/banner.png" alt="D-Modem/<repo>: <tagline>" width="100%">

# <name>

<one line: what it is>

<two or three sentences: what it does and for whom>

- <feature>
- <feature>
- <four to six in all>

## Quick start

<how to install or build it, in a few lines>

## Documentation

The documentation is also a website, [d-modem.github.io/<repo>](https://d-modem.github.io/<repo>/), with reference pages made from the code.

- <the docs index, or the wiki>

## The D-Modem suite

<the shared table of the seven repositories>

## Licence

<one or two lines, with a link to COPYING or LICENSING.md>
```

Until the website of a repository is live, its Documentation section has
a link to the docs index (or the wiki) only.

The suite table is the same in each README:

| Repository | What it is |
| --- | --- |
| [D-Modem](https://github.com/D-Modem/D-Modem) | The open V.92 softmodem: dmodemd, libdmodem and the Asterisk, FreeSWITCH and ARI modules |
| [app](https://github.com/D-Modem/app) | The D-Modem app for Android and iOS: a dial-up modem on a SIP call |
| [hardware](https://github.com/D-Modem/hardware) | pico-serial: RP2040 serial adapters and phone-line USB sticks |
| [menu](https://github.com/D-Modem/menu) | modemmenu: the login and menu dial-up callers reach |
| [bbs](https://github.com/D-Modem/bbs) | A bulletin board for telnet, SSH, TN3270 and modem callers |
| [go3270](https://github.com/D-Modem/go3270) | A Go library for 3270 terminal servers, used by bbs |
| [brand](https://github.com/D-Modem/brand) | Logos, colours, type and the naming guide |
