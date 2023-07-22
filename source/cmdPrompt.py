import asyncio
from main import Scheduler
from DiscordBot import DiscordBot


if __name__ == "__main__":
    cp = cmdPrompt()
    asyncio.run(cp.main())
    exit(0)


class cmdPrompt:
    def __init__():
        self.schedule = Schedule(True, True, True)
        self.dc_bot = DiscordBot()
        
    async def main(self):
        input_task = asyncio.create_task(bot.read_user_input())
        print_task = asyncio.create_task(bot.bot_loop())
        await asyncio.gather(input_task, print_task)

    async def read_user_input(self):
        while True:
            self.usr_cmd = await self.terminal_stats()

    async def terminal_stats(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input)

    async def main(self):
        await asyncio.gather(self.terminal_stats(), self.bot_loop())

    async def bot_loop(self):
        while True:
            self.user_input()
            if self.running:
                self.travel()
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
            print("RESTART")
            self.loc = self.elm.find_locations()
        if self.usr_cmd == "?":
            print("HELP")
            self.print_status()
        if self.usr_cmd == "ss":
            self.screenshot
            

        arguments = self.usr_cmd.split()
        if len(arguments) == 2:
            self.FIGHT_POKEMON = int(arguments[0])
            self.FIGHT_LOCATION = int(arguments[1])
            self.DEFAULT_FIGHT_LOCATION = int(arguments[0])

            print("POKEMON = ", self.team[self.FIGHT_POKEMON])
            print("LOCATION =  ", self.loc[self.FIGHT_LOCATION])
        
        self.usr_cmd = " "

    def screenshot(self):
        current_time = datetime.now().time()
        self.schedule.driver.save_screenshot(f"screenshot{current_time}.png")

    def print_status(self):
        #os.system('cls' if os.name == 'nt' else 'clear')
        if self.running == True:
            print(f'XXXXXX RUNNING XXXXXX')
        else:
            print(f'XXXXXX WAITING XXXXXX')
        print(f'  elm = {self.schedule.elm_status}%')
        print(f'  rezerwa = {self.schedule.rezerwa_count}%')
        print(f'  {self.schedule.FIGHT_POKEMON} | {self.schedule.FIGHT_LOCATION}')
    





# @TODO remake logging system
# @TODO zrobić counter znalezionych itemów/złapanych pokemonów
# @TODO elm quests handling
# @TODO default settings
# @TODO filtrowanie rezerwy
# @TODO przed sprzedażą niech wszystkich ewo

# if text contains "Brawo!" _. you found an item 
# if "nauczyciela" -> TMA
# if "Lidera" -> Lider sali
# EXCEPTION BREAK nie działa
# zoom out - press ctrl - 2 times on start 
# if img in daily contains src "img/items/" ->exception break
# instead of creating a new driver instance, attach it to a active one 
# if found egg -> input name="poluj"  
