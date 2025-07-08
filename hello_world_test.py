import asyncio
import json
import logging
from functools import wraps

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Decorator to log function calls
def log_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f"{func.__name__} returned {result}")
        return result
    return wrapper

# Base greeter class
class Greeter:
    def __init__(self, name="World"):
        self.name = name

    async def greet(self):
        raise NotImplementedError("Subclasses should implement this!")

# Async greeter subclass
class AsyncGreeter(Greeter):

    @log_call
    async def greet(self):
        await asyncio.sleep(1)  # simulate async work
        greeting = f"Hello, {self.name}!"
        print(greeting)
        return greeting

# Function to load config from JSON
def load_config(filepath):
    try:
        with open(filepath, "r") as f:
            config = json.load(f)
            logger.info(f"Config loaded: {config}")
            return config
    except FileNotFoundError:
        logger.error(f"Config file '{filepath}' not found. Using default config.")
        return {"name": "World"}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing config: {e}. Using default config.")
        return {"name": "World"}

async def main():
    config = load_config("config.json")
    greeter = AsyncGreeter(config.get("name", "World"))
    await greeter.greet()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
