use pyo3::prelude::*;

use aho_corasick::{AhoCorasick, AhoCorasickBuilder};

#[pyclass]
struct AC {
    wrappedac: AhoCorasick,
}

#[pymethods]
impl AC {
    #[new]
    fn new(raw_pattern: &str) -> Self {
        let wrappedac = AhoCorasickBuilder::new()
            .dfa(true)
            .build(raw_pattern.split('|'));
        AC { wrappedac }
    }

    fn findall(&self, string: &str) -> PyResult<Vec<usize>> {
        Ok(self
            .wrappedac
            .find_iter(string)
            .map(|mat| mat.pattern())
            .collect())
    }
}

#[pyfunction]
#[pymodule]
fn pyrustac(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AC>()?;
    Ok(())
}
