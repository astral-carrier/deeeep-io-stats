import discord
import logs
from logs import debug
import tools
import commands
from chars import c
import trimmed_embed
import report
import habitat
import commands
import dep_io_stats
from dep_io_stats import DS

class DS_Commands(DS): 
    @DS.command('stats', definite_usages={
        (): 'View your own stats', 
        ('@<user>',): "View `<user>`'s stats", 
        ('<user_ID>',): "Same as above except with Discord ID instead to avoid pings", 
    }) 
    async def check_stats(self, c, m, user=None): 
        if not user: 
            user_id = m.author.id
        else: 
            user_id = self.decode_mention(c, user) 
        
        #debug(user_id) 

        link = None

        if user_id is not None: 
            if not self.blacklisted(c, 'user', user_id): 
                link = self.links_table.find_one(user_id=user_id) 

                #debug('f') 

                if link: 
                    acc_id = link['acc_id'] 

                    if not self.blacklisted(c, 'account', acc_id): 
                        await self.send(c, embed=self.acc_embed(acc_id)) 
                    else: 
                        await self.send(c, content=f'This account (ID {acc_id}) is blacklisted from being displayed on this server. ', reference=m) 
                    
                elif user_id == m.author.id: 
                    await self.send(c, content=f"You're not linked to an account. Type `{self.prefix(c)}link` to learn how to link an account. ", reference=m) 
                else: 
                    await self.send(c, content=f"This user isn't linked.", reference=m) 
            elif user_id == m.author.id: 
                await self.send(c, content=f"You're blacklisted from displaying your account on this server.", reference=m) 
            else: 
                await self.send(c, content='This user is blacklisted from displaying their account on this server. ', reference=m) 
        else: 
            return True
    
    
    @DS.command('blacklist', definite_usages={
        ('user', '<mention>'): 'Blacklist the mentioned user from displaying their Deeeep.io account **on this server only**', 
        ('user', '<user_id>'): 'Like above, but with discord ID instead to avoid pings', 
        ('account', '<account_id>'): 'Blacklists the Deeeep.io account with account ID of `<account_id>` from being displayed **on this server only**', 
        ('map', '<map_id>'): 'Blacklists the map with string ID of `<map_id>` from being displayed **on this server only**', 
    }) 
    @DS.requires_perms(req_one=('manage_messages',)) 
    async def blacklist(self, c, m, blacklist_type, target_str): 
        lower_type = blacklist_type.lower() 

        target = self.convert_target(lower_type, target_str) 

        if target: 
            data = {
                'type': lower_type, 
                'guild_id': c.guild.id, 
                'target': target, 
            } 

            self.blacklists_table.upsert(data, ['type', 'guild_id', 'target'], ensure=True) 

            await self.send(c, content=f'Successfully blacklisted {lower_type} `{target}` on this server.') 
        else: 
            return True
    
    @DS.command('unblacklist', definite_usages={
        ('user', '<mention>'): 'Unblacklist the mentioned user from displaying their Deeeep.io account **on this server only**', 
        ('user', '<user_id>'): 'Like above, but with discord ID instead to avoid pings', 
        ('account', '<account_id>'): 'Unblacklists the Deeeep.io account with account ID of `<account_id>` from being displayed **on this server only**', 
        ('map', '<string_id>'): 'Unblacklists the map with string ID of `<string_id>` from being displayed **on this server only**', 
    }) 
    @DS.requires_perms(req_one=('manage_messages',)) 
    async def unblacklist(self, c, m, blacklist_type, target_str): 
        lower_type = blacklist_type.lower() 

        target = self.convert_target(lower_type, target_str) 

        if target: 
            self.blacklists_table.delete(guild_id=c.guild.id, type=lower_type, target=target) 

            await self.send(c, content=f'Successfully unblacklisted {lower_type} `{target}` on this server.') 
        else: 
            return True
    
    @DS.command('skin', indefinite_usages={
        ('<skin name>',): "View the stats of skin with `<skin name>` (e.g. `Albino Cachalot`)", 
    }) 
    async def check_skin(self, c, m, *skin_query): 
        skin_name = ' '.join(skin_query) 

        skins_list_url = self.SKINS_LIST_URL

        skins_list = self.async_get(skins_list_url)[0] 
        
        if skins_list: 
            skin_data = self.get_skin(skins_list, skin_name) 

            skin_json = None
            suggestions_str = '' 

            if type(skin_data) is list: 
                if len(skin_data) == 1: 
                    skin_json = skin_data[0] 
                else: 
                    if skin_data: 
                        skin_names = (skin['name'] for skin in skin_data) 

                        suggestions_str = tools.format_iterable(skin_names, formatter='`{}`') 

                        suggestions_str = f"Maybe you meant one of these? {suggestions_str}" 
                
                debug(f'Suggestions length: {len(skin_data)}') 
            elif skin_data: 
                skin_json = skin_data

                debug('match found') 
            else: 
                debug('limit exceeded') 

            if skin_json: 
                await self.send(c, embed=self.skin_embed(skin_json)) 
            else: 
                text = "That's not a valid skin name. " + suggestions_str

                await self.send(c, content=text) 
        else: 
            await self.send(c, content=f"Can't fetch skins. Most likely the game is down and you'll need to wait until it's fixed. ") 
    
    @DS.command('skinbyid', definite_usages={
        ('<skin_id>',): 'View the stats of the skin with the given `<skin_id>`', 
    }, public=False) 
    @DS.requires_sb_channel
    async def check_skin_by_id(self, c, m, skin_id): 
        if skin_id.isnumeric(): 
            skin_url = self.SKIN_URL_TEMPLATE.format(skin_id) 

            skin_json = self.async_get(skin_url)[0] 

            if skin_json: 
                await self.send(c, embed=self.skin_embed(skin_json)) 
            else: 
                await self.send(c, content=f"That's not a valid skin ID (or the game might be down).", reference=m) 
        else: 
            return True
    
    @DS.command('map', definite_usages={
        ('<map_string_ID>',): "View the stats of the map with the given `<map_string_ID>` (e.g. `sushuimap_v1`)", 
        ('<map_link>',): "Like above, but using the Mapmaker link of the map instead of the name (e.g. `https://mapmaker.deeeep.io/map/ffa_morty`)"
    }) 
    async def check_map(self, c, m, map_query): 
        map_string_id = self.get_map_string_id(map_query) 

        if map_string_id: 
            map_string_id = self.MAP_URL_ADDITION + map_string_id
            
            map_url = self.MAP_URL_TEMPLATE.format(map_string_id) 

            map_json = self.async_get(map_url)[0] 

            if map_json: 
                ID = map_json['id'] 

                if not self.blacklisted(c, 'map', ID): 
                    await self.send(c, embed=self.map_embed(map_json)) 
                else: 
                    await self.send(c, content=f'This map (ID {ID}) is blacklisted from being displayed on this server. ', reference=m)
            else: 
                await self.send(c, content=f"That's not a valid map (or Mapmaker could be broken). ", reference=m) 
        else: 
            return True
    
    @DS.command('fakerev', definite_usages={
        (): 'Not even Fede knows of the mysterious function of this command...', 
    }, public=False) 
    @DS.requires_owner
    async def fake_review(self, c, m): 
        await self.check_review(c, self.fake_check) 
    
    @DS.command('rev', definite_usages={
        (): 'Not even Fede knows of the mysterious function of this command...', 
    }, public=False) 
    @DS.requires_owner
    async def real_review(self, c, m): 
        rev_channel = self.rev_channel() 

        if rev_channel: 
            await self.check_review(rev_channel, self.real_check, silent_fail=True) 
        else: 
            await self.send(c, content='Not set', reference=m) 
    
    @DS.command('link', definite_usages={
        (): 'View help on linking accounts', 
        ('<account_ID>',): 'Link Deeeep.io account with ID `<account_ID>` to your account', 
        ('<account_profile_pic_URL>',): "Like above, but with the URL of the account's profile picture", 
    }) 
    async def link(self, c, m, query=None): 
        if query: 
            return await self.link_dep_acc(c, m, query) 
        else: 
            await self.link_help(c, m) 
    
    @DS.command('unlink', definite_usages={
        (): 'Unlink your Deeeep.io account', 
    })
    async def unlink(self, c, m): 
        self.links_table.delete(user_id=m.author.id) 

        await self.send(c, content='Unlinked your account. ', reference=m) 
    
    @DS.command('statstest', definite_usages={
        ('<account_ID>',): 'View Deeeep.io account with ID `<account_ID>`', 
        ('<account_profile_pic_URL>',): "Like above, but with the URL of the account's profile picture", 
    }, public=False) 
    @DS.requires_owner
    async def cheat_stats(self, c, m, query): 
        acc_id = self.get_acc_id(query) 
        
        if acc_id is not None: 
            await self.send(c, embed=self.acc_embed(acc_id)) 
        else: 
            return True
    
    @DS.command('prefix', definite_usages={
        ('<prefix>',): "Set the server-wide prefix for this bot to `<prefix>`", 
        (DS.PREFIX_SENTINEL,): f'Reset the server prefix to the default, `{DS.DEFAULT_PREFIX}`', 
    }) 
    @DS.requires_perms(req_one=('manage_messages', 'manage_roles')) 
    async def set_prefix(self, c, m, prefix): 
        if prefix == self.PREFIX_SENTINEL: 
            self.prefixes_table.delete(guild_id=c.guild.id) 

            await self.send(c, content=f'Reset to default prefix `{self.DEFAULT_PREFIX}`') 
        else: 
            if len(prefix) <= self.MAX_PREFIX: 
                data = {
                    'guild_id': c.guild.id, 
                    'prefix': prefix, 
                } 

                self.prefixes_table.upsert(data, ['guild_id'], ensure=True) 

                await self.send(c, content=f'Custom prefix is now `{prefix}`. ') 
            else: 
                await self.send(c, content=f'Prefix must not exceed {self.MAX_PREFIX} characters. ', reference=m) 
    
    @DS.command('revc', definite_usages={
        ('<channel>',): "Sets `<channel>` as the logging channel for skn review", 
        (): 'Like above, but with the current channel', 
        (DS.REV_CHANNEL_SENTINEL,): 'Un-set the logging channel', 
    }, public=False) 
    @DS.requires_owner
    async def set_rev_channel(self, c, m, flag=None): 
        if flag == self.REV_CHANNEL_SENTINEL: 
            self.rev_data_table.delete(key=self.REV_CHANNEL_KEY) 

            await self.send(c, content="Channel removed as the logging channel.") 
        else: 
            if flag is None: 
                channel_id = c.id
            else: 
                channel_id = self.decode_channel(c, flag) 
            
            if channel_id is not None: 
                data = {
                    'key': self.REV_CHANNEL_KEY, 
                    'channel_id': channel_id, 
                } 

                self.rev_data_table.upsert(data, ['key'], ensure=True) 

                await self.send(c, content=f'Set <#{channel_id}> as the logging channel for skin review.') 
            else: 
                return True

    @DS.command('revi', definite_usages={
        ('<i>',): 'Does something', 
    }, public=False) 
    @DS.requires_owner
    async def set_rev_interval(self, c, m, interval): 
        if interval.isnumeric(): 
            seconds = int(interval) 

            data = {
                'key': self.REV_INTERVAL_KEY, 
                'interval': seconds, 
            } 

            self.rev_data_table.upsert(data, ['key'], ensure=True) 

            await self.send(c, content=f'Set interval to {seconds} seconds. ') 
        else: 
            return True
    
    @DS.command('sbchannel', definite_usages={
        ('add', '<channel>'): 'Adds `<channel>` as a Skin Board channel', 
        ('add',): 'Like above, but with the current channel', 
        ('remove', '<channel>'): 'Removes `<channel>` as a Skin Board channel', 
        ('remove',): 'Like above, but with the current channel', 
    }, public=False) 
    @DS.requires_owner
    async def set_sb_channels(self, c, m, flag, channel=None): 
        flag = flag.lower() 

        if channel: 
            channel_id = self.decode_channel(c, channel) 
        else: 
            channel_id = c.id
        
        if channel_id is not None: 
            if flag == 'remove': 
                self.sb_channels_table.delete(channel_id=channel_id) 

                await self.send(c, content=f"<#{channel_id}> removed as a Skin Board channel.") 
            elif flag == 'add': 
                data = {
                    'channel_id': channel_id, 
                } 

                self.sb_channels_table.upsert(data, ['channel_id'], ensure=True) 

                await self.send(c, content=f'Added <#{channel_id}> as a Skin Board channel.') 
            else: 
                return True
        else: 
            return True
    
    @DS.command('pending', indefinite_usages={
        ('<filters>',): f'Get a list of all pending skins in Creators Center that match the filter(s). Valid filters are {DS.FILTERS_STR} or any animal name.', 
    }) 
    @DS.requires_sb_channel
    async def pending_search(self, c, m, *filter_strs): 
        filters = set() 
        filter_strs = set(map(str.lower, filter_strs)) 

        total_filters = {**self.PENDING_FILTERS, **self.ANIMAL_FILTERS} 

        for lowered in filter_strs: 
            if lowered in total_filters: 
                skin_filter = total_filters[lowered] 

                filters.add(skin_filter) 
            else: 
                return True
        
        await self.pending_display(c, filter_strs, filters) 
    
    @DS.command('shutdown', definite_usages={
        (): "Turn off the bot", 
    }, public=False) 
    @DS.requires_owner
    async def shut_down(self, c, m): 
        await self.send(c, content='shutting down') 

        self.logging_out = True

        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='shutting down')) 
    
    @DS.command('help', definite_usages={
        (): 'Get a list of all public commands', 
        ('<command>',): 'Get help on `<command>`', 
    }) 
    async def send_help(self, c, m, command_name=None): 
        if command_name: 
            comm = commands.Command.get_command(command_name)  

            if comm: 
                usage_str = comm.usages_str(self, c, m) 

                await self.send(c, content=f'''How to use the `{command_name}` command: 

{usage_str}''') 
            else: 
                prefix = self.prefix(c) 

                await self.send(c, content=f"That's not a valid command name. Type `{prefix}{self.send_help.name}` for a list of public commands. ", reference=m) 
        else: 
            com_list_str = tools.format_iterable(commands.Command.all_commands(public_only=True), formatter='`{}`') 
            prefix = self.prefix(c) 

            await self.send(c, content=f'''All public commands for this bot: {com_list_str}. 
Type `{prefix}{self.send_help.name} <command>` for help on a specified `<command>`''') 
    
    @DS.command('info', definite_usages={
        (): 'Display info about this bot', 
    }) 
    async def send_info(self, c, m): 
        await self.send(c, embed=await self.self_embed(c)) 