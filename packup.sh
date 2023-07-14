archive_name=archive.7z
rm -rf $archive_name
find . | grep -E ".+(py|j2|json|txt)\$" | xargs -Iabc 7z a $archive_name abc