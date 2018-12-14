#[macro_use]
extern crate warp;

use std::env;

use env_logger as logger;
use log::*;
use serde_derive::*;
use snips_nlu_lib::SnipsNluEngine;
use warp::Filter;

#[derive(Deserialize, Serialize)]
struct ParseRequest {
    text: String,
}

fn main() {
    if env::var_os("RUST_LOG").is_none() {
        env::set_var("RUST_LOG", "nlu=info,warp=debug");
    }
    logger::init();

    let parse = path!("parse")
        .and(warp::body::content_length_limit(1024 * 1024 * 1024))
        .and(warp::body::json())
        .map(|req: ParseRequest| {
            // TODO: figure out how to borrow engine so we don't have to load it every time
            let engine = SnipsNluEngine::from_path("model/engine/").unwrap();
            debug!("Loaded the nlu engine...");

            let result = engine.parse(req.text.trim(), None).unwrap();
            info!("{:?}", &result);

            warp::reply::json(&result)
        });

    warp::serve(parse).run(([0, 0, 0, 0], 9001));
}
