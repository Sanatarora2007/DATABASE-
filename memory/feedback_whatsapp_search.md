---
name: WhatsApp Search Strategy
description: Always use SQLite directly for WhatsApp searches except for recent/latest messages
type: feedback
---

Always query the WhatsApp SQLite databases directly. **Never touch MCP tools first.**

**Databases:**
- Contacts: `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ContactsV2.sqlite` → table `ZWAADDRESSBOOKCONTACT` (columns: ZFULLNAME, ZPHONENUMBER)
- Chats/Messages: `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite` → tables `ZWAMESSAGE`, `ZWACHATSESSION`, `ZWAMEDIAITEM`
- Chat JID lookup: `ZWACHATSESSION.ZCONTACTJID` and `ZWACHATSESSION.ZPARTNERNAME`
- Media local path: `ZWAMEDIAITEM.ZMEDIALOCALPATH` (relative to `.../Message/` directory)

**Why:** MCP tools return incomplete data (numeric IDs instead of names, empty results for contacts). SQLite is always the authoritative source and returns full structured data.

**Rule:**
- ANY WhatsApp task (find contact, search messages, find media, find chat) → SQLite first, always
- "Latest" / "last message" under ~1 hour → SQLite first, then MCP as a supplement only if needed
- Never open with MCP list_chats, search_contacts, or list_messages — these are fallbacks only

**How to apply:** The moment the user mentions WhatsApp, go straight to sqlite3. Do not call a single MCP tool before checking SQLite.
