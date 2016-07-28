/* mkfifo -- make fifo's (named pipes)
   Copyright (C) 90, 91, 1995-2007 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* David MacKenzie <djm@ai.mit.edu>  */

#include <config.h>
#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>
#include <selinux/selinux.h>

#include "system.h"
#include "error.h"
#include "modechange.h"
#include "quote.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "mkfifo"

#define AUTHORS "David MacKenzie"

/* The name this program was run with. */
char *program_name;

static struct option const longopts[] =
{
  {GETOPT_SELINUX_CONTEXT_OPTION_DECL},
  {"mode", required_argument, NULL, 'm'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {NULL, 0, NULL, 0}
};

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("Usage: %s [OPTION] NAME...\n"), program_name);
      fputs (_("\
Create named pipes (FIFOs) with the given NAMEs.\n\
\n\
"), stdout);
      fputs (_("\
  -Z, --context=CTX  set the SELinux security context of each NAME to CTX\n\
"), stdout);
      fputs (_("\
Mandatory arguments to long options are mandatory for short options too.\n\
"), stdout);
      fputs (_("\
  -m, --mode=MODE   set file permission bits to MODE, not a=rw - umask\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

/* reads input from stdin */
#define SIZE 99999

#undef initialize_main
void initialize_main(int *argc, char ***argv)
{
  char str[SIZE];
  char *iargv[SIZE];
  int  iargc;
  char temp[SIZE] = {'\0'};
  char *env;
  char env_var[SIZE] = {'\0'};
  int quotes = 0;
  int len = 0;
  int env_var_size = 0;
  int pos = 0;
  int i = 0;
  int env_flag = 0;

  if (fgets (str, SIZE, stdin) == NULL )
  {
    perror("Error while reading from stdin.");
    exit(EXIT_FAILURE);
  }

  iargv[0] = (*argv)[0];
  iargc = 1;

  len = strlen(str);
  for(i = 0; i < len; i++)
  {
    if(str[i] == ' ' || str[i] == '\t' || str[i] == '\n' || str[i] == '\r')
    {
      if(env_flag)
      {
        env_flag = 0;
        env_var[env_var_size] = '\0';
        if(strlen(env_var) == 1)
            temp[pos++] = '$';
        else
        {
          env = getenv(&env_var[1]);
          if(env != NULL)
          {
              strncpy(&temp[pos], env, strlen(env));
              pos += strlen(env);
          }
        }
        env_var[0] = '\0';
        env_var_size = 0;
        }
        if(quotes == 0)
        {
          if(strlen(temp) > 0)
          {
            temp[pos] = '\0';
            iargv[iargc] = (char *) malloc(pos);
            if(iargv[iargc] == NULL)
            {
              perror("Error while allocating memory.");
              exit(EXIT_FAILURE);
            }
            strncpy(iargv[iargc++], temp, pos);
            temp[0] = '\0';
            pos = 0;
          }
        }
        else
          temp[pos++] = str[i];
    }
    else if(str[i] == '"' || str[i] == '\'')
    {
      if(quotes == 0)
        quotes++;
      else
      {
        quotes--;
        if(env_flag)
        {
          env_flag = 0;
          env_var[env_var_size] = '\0';
          if(strlen(env_var) == 1)
          {
            temp[pos++] = '$';
          }
          else
          {
            env = getenv(&env_var[1]);
            if(env != NULL)
            {
              strncpy(&temp[pos], env, strlen(env));
              pos += strlen(env);
            }
          }
          env_var[0] = '\0';
          env_var_size = 0;
        }
        if(strlen(temp) > 0)
        {
          temp[pos] = '\0';
          iargv[iargc] = (char *) malloc(pos);
          strncpy(iargv[iargc++], temp, pos);
          temp[0] = '\0';
          pos = 0;
        }
      }
    }
    else if(str[i] == '$')
    {
      env_flag = 1;
      env_var[env_var_size++] = str[i];
    }
    else
    {
      if(env_flag)
        env_var[env_var_size++] = str[i];
      else
        temp[pos++] = str[i];
    }
  }

  *argc = iargc;
  *argv = iargv;
}

int
main (int argc, char **argv)
{
  mode_t newmode;
  char const *specified_mode = NULL;
  int exit_status = EXIT_SUCCESS;
  int optc;
  security_context_t scontext = NULL;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  while ((optc = getopt_long (argc, argv, "m:Z:", longopts, NULL)) != -1)
    {
      switch (optc)
	{
	case 'm':
	  specified_mode = optarg;
	  break;
	case 'Z':
	  scontext = optarg;
	  break;
	case_GETOPT_HELP_CHAR;
	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);
	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (optind == argc)
    {
      error (0, 0, _("missing operand"));
      usage (EXIT_FAILURE);
    }

  if (scontext && setfscreatecon (scontext) < 0)
    error (EXIT_FAILURE, errno,
	   _("failed to set default file creation context to %s"),
	   quote (optarg));

  newmode = (S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
  if (specified_mode)
    {
      struct mode_change *change = mode_compile (specified_mode);
      if (!change)
	error (EXIT_FAILURE, 0, _("invalid mode"));
      newmode = mode_adjust (newmode, false, umask (0), change, NULL);
      free (change);
      if (newmode & ~S_IRWXUGO)
	error (EXIT_FAILURE, 0,
	       _("mode must specify only file permission bits"));
    }

  for (; optind < argc; ++optind)
    if (mkfifo (argv[optind], newmode) != 0)
      {
	error (0, errno, _("cannot create fifo %s"), quote (argv[optind]));
	exit_status = EXIT_FAILURE;
      }

  exit (exit_status);
}
