fn subseq<A: PartialEq>(s: &[A], t: &[A]) -> Option<usize> {
    for i in 0..=(t.len().saturating_sub(s.len())) {
        if s == &t[i..i + s.len()] {
            return Some(i);
        }
    }
    None
}

fn replace<A: PartialEq + Clone>(s: &[A], lhs: &[A], rhs: &[A]) -> Vec<A> {
    if let Some(i) = subseq(lhs, s) {
        let mut result = Vec::new();
        result.extend_from_slice(&s[..i]);
        result.extend_from_slice(rhs);
        result.extend_from_slice(&s[i + lhs.len()..]);
        result
    } else {
        s.to_vec()
    }
}



#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_subseq() {
        assert_eq!(subseq(&[2, 2], &[1, 1, 1, 2, 2]), Some(3));
        assert_eq!(subseq(&[2, 2], &[1, 1, 1, 2, 2, 2]), Some(3));
        assert_eq!(subseq(&[], &[1, 2, 3]), Some(0));
        assert_eq!(subseq(&[3, 4], &[4, 5, 3]), None);
        assert_eq!(subseq(&[3, 4], &[4, 5, 3, 4]), Some(2));
    }

    #[test]
    fn test_replace() {
        assert_eq!(replace(&[1, 2, 3, 4], &[2, 3], &[5, 6]), vec![1, 5, 6, 4]);
        assert_eq!(replace(&[1, 2, 3, 4], &[2, 3], &[5, 6, 7]), vec![1, 5, 6, 7, 4]);
        assert_eq!(replace(&[1, 2, 3, 4], &[2, 3], &[5, 6, 7, 8]), vec![1, 5, 6, 7, 8, 4]);
        assert_eq!(replace(&[1, 1], &[4, 4], &[2, 2]), vec![1, 1]);
    }
}



fn main() {
    println!("Hello, world!");
}
