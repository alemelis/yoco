use indicatif::ProgressBar;
use indicatif::ProgressStyle;
use pyo3::prelude::*;
use std::path::Path;

#[pyfunction]
fn check_ann(s: &str, num_classes: i32) -> bool {
    if s.is_empty() {
        return true;
    }

    let data: Vec<&str> = s.split(" ").collect();
    if data.len() != 5 {
        return false;
    }

    let c = match data[0].parse::<i32>() {
        Ok(val) => val,
        Err(_) => return false,
    };
    if c >= num_classes || c < 0 {
        return false;
    }

    let x = match data[1].parse::<f32>() {
        Ok(val) => val,
        Err(_) => return false,
    };
    if x < 0.0 || x >= 1.0 {
        return false;
    }

    let y = match data[2].parse::<f32>() {
        Ok(val) => val,
        Err(_) => return false,
    };
    if y < 0.0 || y >= 1.0 {
        return false;
    }

    let w = match data[3].parse::<f32>() {
        Ok(val) => val,
        Err(_) => return false,
    };
    if w <= 0.0 || w > 1.0 {
        return false;
    }

    let h = match data[4].parse::<f32>() {
        Ok(val) => val,
        Err(_) => return false,
    };
    if h <= 0.0 || h > 1.0 {
        return false;
    }

    if x + w > 1.0 || y + h > 1.0 {
        return false;
    }

    true
}

#[pyfunction]
fn check_ann_file(path_str: &str, num_classes: i32) -> bool {
    let p = Path::new(path_str);
    if !p.exists() {
        return false;
    }

    let content = match std::fs::read_to_string(p) {
        Ok(val) => val,
        Err(_) => return false,
    };

    if content.is_empty() {
        return true;
    }

    let lines: Vec<&str> = content.split("\n").collect();
    for line in lines {
        if !check_ann(line.trim(), num_classes) {
            return false;
        }
    }

    true
}

#[pyfunction]
fn validate_list(py: Python<'_>, path_str: &str, num_classes: i32) -> PyResult<()> {
    println!("Checking annotation file in rust...");

    let pil = py.import("PIL.Image")?;

    let p = Path::new(path_str);
    if !p.exists() {
        return Ok(());
    }

    let content = match std::fs::read_to_string(p) {
        Ok(val) => val,
        Err(_) => return Ok(()),
    };

    if content.is_empty() {
        return Ok(());
    }

    let lines: Vec<&str> = content.split("\n").collect();
    let mut good_ims: Vec<&str> = Vec::new();
    let mut bad_ims: Vec<&str> = Vec::new();
    let pb = ProgressBar::new(lines.len() as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template(
                "{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta}) {per_sec}",
            )
            .unwrap()
            .progress_chars("#>-"),
    );
    for line in lines {
        let img_path = line.trim();
        let ann_file = img_path.replace("/ims/", "/anns/");
        if !check_ann_file(&ann_file, num_classes) {
            bad_ims.push(line);
        } else {
            let img_valid = match pil.getattr("open")?.call1((img_path,)) {
                Ok(_) => true,
                Err(_) => false,
            };

            if img_valid {
                good_ims.push(line);
            } else {
                bad_ims.push(line);
            }
        }

        pb.inc(1);
    }
    pb.finish_with_message("Validation complete");

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn yoco(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(check_ann, m)?)?;
    m.add_function(wrap_pyfunction!(check_ann_file, m)?)?;
    m.add_function(wrap_pyfunction!(validate_list, m)?)?;
    Ok(())
}
