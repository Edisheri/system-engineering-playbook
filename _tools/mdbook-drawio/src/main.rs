use mdbook::preprocess::{Preprocessor, PreprocessorContext};
use mdbook::book::{Book, BookItem};
use regex::Regex;
use std::io;
use serde_json;

pub struct DrawioPreprocessor;

impl DrawioPreprocessor {
    pub fn new() -> DrawioPreprocessor {
        DrawioPreprocessor
    }

    fn convert_github_to_raw(&self, github_url: &str) -> String {
        github_url
            .replace("github.com", "raw.githubusercontent.com")
            .replace("/blob/", "/")
    }

    fn create_iframe(&self, url: &str) -> String {
        let raw_url = self.convert_github_to_raw(url);
        format!(
            r#"<iframe class="drawio-viewer" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url={}"></iframe>"#,
            raw_url
        )
    }
}

impl Preprocessor for DrawioPreprocessor {
    fn name(&self) -> &str {
        "drawio"
    }

    fn run(&self, ctx: &PreprocessorContext, mut book: Book) -> Result<Book, mdbook::errors::Error> {
        // Поддержка GitHub URLs
        let github_regex = Regex::new(r"@drawio\{(https://github\.com/[^\s}]+\.drawio)\}").unwrap();
        
        // Поддержка локальных файлов (относительные пути от src/)
        let local_regex = Regex::new(r"@drawio\{\.\./diagrams-codes/([^\s}]+\.drawio)\}").unwrap();
        
        book.for_each_mut(|item| {
            if let BookItem::Chapter(chapter) = item {
                // Обработка GitHub URLs
                chapter.content = github_regex.replace_all(&chapter.content, |caps: &regex::Captures| {
                    self.create_iframe(&caps[1])
                }).to_string();
                
                // Обработка локальных файлов - конвертируем в GitHub URL для viewer
                chapter.content = local_regex.replace_all(&chapter.content, |caps: &regex::Captures| {
                    let filename = &caps[1];
                    // Используем GitHub URL для viewer (будет работать после push)
                    let github_url = format!("https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/{}", filename);
                    self.create_iframe(&github_url)
                }).to_string();
            }
        });

        Ok(book)
    }
}

fn main() -> Result<(), mdbook::errors::Error> {
    let preprocessor = DrawioPreprocessor::new();
    let args: Vec<String> = std::env::args().collect();

    if args.len() >= 2 && args[1] == "supports" {
        std::process::exit(0);
    }

    let (ctx, book) = mdbook::preprocess::CmdPreprocessor::parse_input(io::stdin())?;
    let processed_book = preprocessor.run(&ctx, book)?;
    
    serde_json::to_writer(io::stdout(), &processed_book)?;

    Ok(())
}