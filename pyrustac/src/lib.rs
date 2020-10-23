// Inspired by https://stackoverflow.com/a/57129532/6214034

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use aho_corasick::AhoCorasick;

#[pyfunction]
fn ahocorasick(string: &str, raw_pattern: &str) -> PyResult<Vec<usize>> {
    let ac = AhoCorasick::new(raw_pattern.split('|'));

    Ok(ac.find_iter(string).map(|mat| mat.start()).collect())
}

#[pymodule]
fn pyrustac(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ahocorasick, m)?)?;
    Ok(())
}
