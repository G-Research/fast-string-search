use aho_corasick::{AhoCorasick, AhoCorasickBuilder};
use flashtext::KeywordProcessor;
use pyo3::prelude::*;
use std::collections::HashSet;

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

#[pyclass]
struct FT {
    wrappedft: KeywordProcessor,
}

#[pymethods]
impl FT {
    #[new]
    fn new() -> Self {
        // Case sensitive by default?
        FT {
            wrappedft: KeywordProcessor::new(true),
        }
    }

    fn add(&mut self, string: &str) -> PyResult<()> {
        self.wrappedft.add_keyword(string);
        Ok(())
    }

    fn find_keywords(&self, input: &str) -> PyResult<HashSet<String>> {
        Ok(self.wrappedft.find_keywords(input))
    }
}

#[pyfunction]
#[pymodule]
fn pyrustac(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AC>()?;
    m.add_class::<FT>()?;
    Ok(())
}
