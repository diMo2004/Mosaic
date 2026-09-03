class PlaceholderOCRProvider:
    def extract_text(self, file) -> str:
        name = getattr(file, "name", "")

        if name.endswith(".txt"):
            file.open("rb")
            content = file.read().decode("utf-8", errors="ignore")
            file.close()
            return content

        return "Placeholder OCR text. Replace this with the selected OCR provider."