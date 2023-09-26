# old stuff, might be usefull soon 2023-07-25 12:52


    async def main(self):
        #input_task = asyncio.create_task(self.terminal_stats())
        print_task = asyncio.create_task(self.bot_loop())
        await asyncio.gather(input_task, print_task)
    
    # chyba do wywalenia
    #async def read_user_input(self):
    #    while True:
    #        self.usr_cmd = await self.terminal_stats()

    async def terminal_stats(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input)

    async def bot_loop(self):
        while True:
            self.user_input()
            if self.running:
                self.schedule.travel()
            await asyncio.sleep(0.1)

    def user_input(self):
        if len(self.usr_cmd) < 2:
            return
        if self.usr_cmd == "stop":
            print("STOP")
            self.running = False
        if self.usr_cmd == "start":
            print("START")
            self.running = True 
        if self.usr_cmd == "restart":
        f self.usr_cmd == "?":
            self.print_status()
        if self.usr_cmd == "ss":
            self.screenshot()
         
