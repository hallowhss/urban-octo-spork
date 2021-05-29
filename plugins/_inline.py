# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import re
import time
from datetime import datetime
from math import ceil
from os import remove
from platform import python_version as PyVer

from git import Repo
from pyUltroid import __version__ as UltVer
from support import *
from telethon import Button, __version__
from telethon.tl.types import InputWebDocument

from . import *

# ================================================#
notmine = f"This bot is for {OWNER_NAME}"
ULTROID_PIC = "https://telegra.ph/file/115f149ed8e154641708b.jpg"
helps = get_string("inline_1")

add_ons = udB.get("ADDONS")
if add_ons == "True" or add_ons is None:
    zhelps = get_string("inline_2")
else:
    zhelps = get_string("inline_3")
if udB.get("INLINE_PIC"):
    _file_to_replace = udB.get("INLINE_PIC")
else:
    _file_to_replace = "resources/extras/inline.jpg"
# ============================================#


@in_pattern("")
@in_owner
async def e(o):
    if len(o.text) == 0:
        b = o.builder
        uptime = grt(time.time() - start_time)
        header = udB.get("ALIVE_TEXT") if udB.get("ALIVE_TEXT") else "Hey,  I am alive."
        ALIVEMSG = get_string("alive_1").format(
            header,
            OWNER_NAME,
            OWNER_ID,
            ultroid_version,
            uptime,
            PyVer(),
            Repo().active_branch,
        )
        res = [
            await b.article(
                title="Ultroid Userbot",
                url="https://t.me/TeamUltroid",
                description="Userbot | Telethon ",
                text=ALIVEMSG,
                thumb=InputWebDocument(ULTROID_PIC, 0, "image/jpeg", []),
                buttons=[
                    [Button.url(text="Support Group", url="t.me/UltroidSupport")],
                    [
                        Button.url(
                            text="Repo",
                            url="https://github.com/Teamultroid/Ultroid",
                        ),
                    ],
                ],
            ),
        ]
        await o.answer(res, switch_pm=f"👥 ULTROID PORTAL", switch_pm_param="start")


@in_pattern("ultd")
@in_owner
async def inline_handler(event):
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    cmd = len(z)
    bnn = asst.me.username
    result = event.builder.photo(
        file=_file_to_replace,
        link_preview=False,
        text=get_string("inline_4").format(
            len(PLUGINS),
            len(ADDONS),
            cmd,
        ),
        buttons=[
            [
                Button.inline("Plugins", data="hrrrr"),
                Button.inline("Addons", data="frrr"),
            ],
            [
                Button.inline("Ferramentas de Owner", data="ownr"),
                Button.inline("Inline Plugins", data="inlone"),
            ],
            [
                Button.url("Opções", url=f"https://t.me/{bnn}?start=set"),
            ],
            [Button.inline("Fechar", data="close")],
        ],
    )
    await event.answer([result])


@in_pattern("paste")
@in_owner
async def _(event):
    ok = event.text.split(" ")[1]
    link = "https://nekobin.com/"
    result = event.builder.article(
        title="Paste",
        text="Pᴀsᴛᴇᴅ Tᴏ Nᴇᴋᴏʙɪɴ!",
        buttons=[
            [
                Button.url("NekoBin", url=f"{link}{ok}"),
                Button.url("Raw", url=f"{link}raw/{ok}"),
            ],
        ],
    )
    await event.answer([result])


@callback("ownr")
@owner
async def setting(event):
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    cmd = len(z)
    await event.edit(
        get_string("inline_4").format(
            len(PLUGINS),
            len(ADDONS),
            cmd,
        ),
        file=_file_to_replace,
        link_preview=False,
        buttons=[
            [
                Button.inline("Ping", data="pkng"),
                Button.inline("Uptime", data="upp"),
            ],
            [
                Button.inline("Reiniciar", data="rstrt"),
                Button.inline("Atualizar", data="doupdate"),
            ],
            [Button.inline("⬅ Voltar", data="open")],
        ],
    )


@callback("doupdate")
@owner
async def _(event):
    check = await updater()
    if not check:
        return await event.answer(
            "Você já está na última versão!", cache_time=0, alert=True
        )
    repo = Repo.init()
    ac_br = repo.active_branch
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    changelog_str = changelog + f"\n\nClique no botão abaixo para atualizar!"
    if len(changelog_str) > 1024:
        await event.edit(get_string("upd_4"))
        file = open(f"excalibur_update.txt", "w+")
        file.write(tl_chnglog)
        file.close()
        await event.edit(
            get_string("upd_5"),
            file="excalibur_update.txt",
            buttons=[
                [Button.inline("Atualizar agora", data="updatenow")],
                [Button.inline("⬅ Voltar", data="ownr")],
            ],
        )
        remove(f"excalibur_update.txt")
        return
    else:
        await event.edit(
            changelog_str,
            buttons=[
                [Button.inline("Atualizar agora", data="updatenow")],
                [Button.inline("⬅ Voltar", data="ownr")],
            ],
            parse_mode="html",
        )


@callback("pkng")
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    pin = f"🌋 Ping = {ms}ms"
    await event.answer(pin, cache_time=0, alert=True)


@callback("upp")
async def _(event):
    uptime = grt(time.time() - start_time)
    pin = f"🙋 Uptime = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


@callback("inlone")
@owner
async def _(e):
    button = [
        [
            Button.switch_inline(
                "Play Store Apps",
                query="app telegram",
                same_peer=True,
            ),
            Button.switch_inline(
                "Apps Modificados",
                query="mods minecraft",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "Pesquisa no Google",
                query="go GitHub",
                same_peer=True,
            ),
            Button.switch_inline(
                "Pesquisa no Yahoo",
                query="yahoo GitHub",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "Whisper",
                query="msg @username wspr Olá!",
                same_peer=True,
            ),
            Button.switch_inline(
                "Youtube Downloader",
                query="yt Chatuba de Mesquita",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "Pesquisa de Imagem",
                query="clipart sapo",
                same_peer=True,
            ),
            Button.switch_inline(
                "OrangeFox",
                query="ofox ginkgo",
                same_peer=True,
            ),
        ],
        [
            Button.inline(
                "⬅ Voltar",
                data="open",
            ),
        ],
    ]
    await e.edit(buttons=button, link_preview=False)


@callback("hrrrr")
@owner
async def on_plug_in_callback_query_handler(event):
    xhelps = helps.format(OWNER_NAME, len(PLUGINS))
    buttons = page_num(0, PLUGINS, "helpme", "def")
    await event.edit(f"{xhelps}", buttons=buttons, link_preview=False)


@callback("frrr")
@owner
async def addon(event):
    halp = zhelps.format(OWNER_NAME, len(ADDONS))
    if len(ADDONS) > 0:
        buttons = page_num(0, ADDONS, "addon", "add")
        await event.edit(f"{halp}", buttons=buttons, link_preview=False)
    else:
        await event.answer(
            f"• Tʏᴘᴇ `{HNDLR}setredis ADDONS True`\n Tᴏ ɢᴇᴛ ᴀᴅᴅᴏɴs ᴘʟᴜɢɪɴs",
            cache_time=0,
            alert=True,
        )


@callback("rstrt")
@owner
async def rrst(ult):
    await restart(ult)


@callback(
    re.compile(
        rb"helpme_next\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number + 1, PLUGINS, "helpme", "def")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"helpme_prev\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number - 1, PLUGINS, "helpme", "def")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"addon_next\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number + 1, ADDONS, "addon", "add")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"addon_prev\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number - 1, ADDONS, "addon", "add")
    await event.edit(buttons=buttons, link_preview=False)


@callback("back")
@owner
async def backr(event):
    xhelps = helps.format(OWNER_NAME, len(PLUGINS))
    current_page_number = int(upage)
    buttons = page_num(current_page_number, PLUGINS, "helpme", "def")
    await event.edit(
        f"{xhelps}",
        file=_file_to_replace,
        buttons=buttons,
        link_preview=False,
    )


@callback("buck")
@owner
async def backr(event):
    xhelps = zhelps.format(OWNER_NAME, len(ADDONS))
    current_page_number = int(upage)
    buttons = page_num(current_page_number, ADDONS, "addon", "add")
    await event.edit(
        f"{xhelps}",
        file=_file_to_replace,
        buttons=buttons,
        link_preview=False,
    )


@callback("open")
@owner
async def opner(event):
    bnn = asst.me.username
    buttons = [
        [
            Button.inline("Plugins ", data="hrrrr"),
            Button.inline("Addons", data="frrr"),
        ],
        [
            Button.inline("Ferramentas", data="ownr"),
            Button.inline("Inline Plugins", data="inlone"),
        ],
        [
            Button.url(
                "Opções",
                url=f"https://t.me/{bnn}?start={ultroid_bot.me.id}",
            ),
        ],
        [Button.inline("••Cʟᴏꜱᴇ••", data="close")],
    ]
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    cmd = len(z) + 10
    await event.edit(
        get_string("inline_4").format(
            OWNER_NAME,
            len(PLUGINS),
            len(ADDONS),
            cmd,
        ),
        buttons=buttons,
        link_preview=False,
    )


@callback("close")
@owner
async def on_plug_in_callback_query_handler(event):
    await event.edit(
        get_string("inline_5"),
        file=_file_to_replace,
        buttons=Button.inline("Abrir novamente", data="open"),
    )


@callback(
    re.compile(
        b"def_plugin_(.*)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = f"Nome do Plugin: `{plugin_name}`\n"
    try:
        for i in HELP[plugin_name]:
            help_string += i
    except BaseException:
        pass
    if help_string == "":
        reply_pop_up_alert = f"{plugin_name} has no detailed help..."
    else:
        reply_pop_up_alert = help_string
    reply_pop_up_alert += "\n© @TeamUltroid"
    buttons = [
        [
            Button.inline(
                "⬅ Enviar Plugin ➡",
                data=f"sndplug_{(event.data).decode('UTF-8')}",
            )
        ],
        [
            Button.inline("⬅ Voltar", data="back"),
            Button.inline("Fechar", data="close"),
        ],
    ]
    try:
        if event.query.user_id in sed:
            await event.edit(
                reply_pop_up_alert,
                buttons=buttons,
            )
        else:
            reply_pop_up_alert = notmine
            await event.answer(reply_pop_up_alert, cache_time=0)
    except BaseException:
        halps = f"Do .help {plugin_name} to get the list of commands."
        await event.edit(halps, buttons=buttons)


@callback(
    re.compile(
        b"add_plugin_(.*)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = ""
    try:
        for i in HELP[plugin_name]:
            help_string += i
    except BaseException:
        try:
            for u in CMD_HELP[plugin_name]:
                help_string = f"Nome do Plugin:{plugin_name}\n\n❗ Comandos Disponíveis: \n\n"
                help_string += str(CMD_HELP[plugin_name])
        except BaseException:
            try:
                if plugin_name in LIST:
                    help_string = (
                        f"Nome do Plugin:{plugin_name}\n\n❗ Comandos Disponíveis: \n\n"
                    )
                    for d in LIST[plugin_name]:
                        help_string += HNDLR + d
                        help_string += "\n"
            except BaseException:
                pass
    if help_string == "":
        reply_pop_up_alert = f"{plugin_name} has no detailed help..."
    else:
        reply_pop_up_alert = help_string
    reply_pop_up_alert += "\n© @TeamUltroid"
    buttons = [
        [
            Button.inline(
                "⬅ Enviar Plugin ➡",
                data=f"sndplug_{(event.data).decode('UTF-8')}",
            )
        ],
        [
            Button.inline("⬅ Voltar", data="buck"),
            Button.inline("Fechar", data="close"),
        ],
    ]
    try:
        if event.query.user_id in sed:
            await event.edit(
                reply_pop_up_alert,
                buttons=buttons,
            )
        else:
            reply_pop_up_alert = notmine
            await event.answer(reply_pop_up_alert, cache_time=0)
    except BaseException:
        halps = f"Do .help {plugin_name} to get the list of commands."
        await event.edit(halps, buttons=buttons)


def page_num(page_number, loaded_plugins, prefix, type):
    number_of_rows = 5
    number_of_cols = 2
    emoji = Redis("EMOJI_IN_HELP")
    if emoji:
        multi = emoji
    else:
        multi = "🔴"
    helpable_plugins = []
    global upage
    upage = page_number
    for p in loaded_plugins:
        helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        Button.inline(
            "{} {} {}".format(
                multi,
                x,
                multi,
            ),
            data=f"{type}_plugin_{x}",
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "⬅ Anterior",
                    data=f"{prefix}_prev({modulo_page})",
                ),
                Button.inline("« Bᴀᴄᴋ »", data="open"),
                Button.inline(
                    "Próximo ➡",
                    data=f"{prefix}_next({modulo_page})",
                ),
            ),
        ]
    else:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [(Button.inline("⬅ Voltar ➡", data="open"),)]
    return pairs
