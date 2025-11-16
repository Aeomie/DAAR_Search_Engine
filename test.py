from engine import engine_text

result = engine_text(
    pattern="hello",
    text="hello world, hello again!",
    mode="regex"
)

print(result)
