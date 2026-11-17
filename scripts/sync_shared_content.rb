#!/usr/bin/env ruby

require "fileutils"
require "pathname"

ROOT = Pathname.new(__dir__).join("..").expand_path
SHARED_BIBLIOGRAPHY = ROOT.join("shared/publications.bib")
SHARED_NEWS = ROOT.join("shared/news")
TARGETS = [ROOT, ROOT.join("lab")].freeze

check_only = ARGV.delete("--check")
abort "Usage: #{File.basename($PROGRAM_NAME)} [--check]" unless ARGV.empty?

def same_file?(source, target)
  target.file? && FileUtils.compare_file(source.to_s, target.to_s)
end

def relative(path)
  path.relative_path_from(ROOT).to_s
end

drift = []

TARGETS.each do |site|
  bibliography = site.join("_bibliography/papers.bib")
  news_directory = site.join("_news")
  shared_news_files = SHARED_NEWS.glob("*.md").sort
  target_news_files = news_directory.glob("*.md").sort

  if check_only
    drift << relative(bibliography) unless same_file?(SHARED_BIBLIOGRAPHY, bibliography)

    shared_names = shared_news_files.map(&:basename)
    target_names = target_news_files.map(&:basename)
    drift << relative(news_directory) unless shared_names == target_names

    shared_news_files.each do |source|
      target = news_directory.join(source.basename)
      drift << relative(target) unless same_file?(source, target)
    end
    next
  end

  FileUtils.mkdir_p(bibliography.dirname)
  FileUtils.cp(SHARED_BIBLIOGRAPHY, bibliography)

  FileUtils.mkdir_p(news_directory)
  shared_names = shared_news_files.map { |path| path.basename.to_s }
  target_news_files.each do |target|
    FileUtils.rm_f(target) unless shared_names.include?(target.basename.to_s)
  end
  shared_news_files.each { |source| FileUtils.cp(source, news_directory.join(source.basename)) }
end

if check_only
  if drift.empty?
    puts "Shared publications and news are synchronized."
  else
    warn "Shared content is out of sync:"
    drift.uniq.sort.each { |path| warn "  - #{path}" }
    warn "Run ruby scripts/sync_shared_content.rb and commit the generated files."
    exit 1
  end
else
  puts "Synchronized publications and news for taohu.me and taohu.me/lab."
end
