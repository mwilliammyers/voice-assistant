use std::env;

use serde_json as json;
use snips_nlu_lib::SnipsNluEngine;

fn main() {
    if let Some(query) = env::args().nth(1) {
       let engine =  match env::args().nth(2) {
            Some(path) =>  SnipsNluEngine::from_path(path).unwrap(),
            _ =>  SnipsNluEngine::from_path("model/engine/").unwrap(),
        };

        let result = engine.parse(query.trim(), None).unwrap();
       
        println!("{}", json::to_string(&result).unwrap());
    }
}
