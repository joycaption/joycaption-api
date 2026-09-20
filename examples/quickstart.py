        """Minimal JoyCaption example: create one prediction and print the output URL(s)."""
        import joycaption_api

        output = joycaption_api.run({
    "image": "https://example.com/input.png",
    "prompt": "Are you allowed to swim here?"
})
        print(output)
